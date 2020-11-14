/**
 * 
 * Name: chengsa
 * Student ID: 1170300512
 */

#include <memory>
#include <iostream>
#include "buffer.h"
#include "exceptions/buffer_exceeded_exception.h"
#include "exceptions/page_not_pinned_exception.h"
#include "exceptions/page_pinned_exception.h"
#include "exceptions/bad_buffer_exception.h"
#include "exceptions/hash_not_found_exception.h"

namespace badgerdb {

//----------------------------------------
// Constructor of the class BufMgr
//----------------------------------------

    BufMgr::BufMgr(std::uint32_t bufs)
            : numBufs(bufs) {
        bufDescTable = new BufDesc[bufs];

        for (FrameId i = 0; i < bufs; i++)
        {
            bufDescTable[i].frameNo = i;
            bufDescTable[i].valid = false;
        }

        bufPool = new Page[bufs];

        int htsize = ((((int) (bufs * 1.2))*2)/2)+1;
        hashTable = new BufHashTbl (htsize);  // allocate the buffer hash table

        clockHand = bufs - 1;
    }

//
////清除缓冲池,检查dirty页写回disk,释放空间
//
    BufMgr::~BufMgr() {
        //check for any dirty pages that need to be flushed to disk
        for (unsigned i = 0; i < numBufs; i++) {
            BufDesc* buf = &bufDescTable[i];
            //检查dirty页
            if (buf->dirty == 1){
                buf->file->writePage(bufPool[buf->frameNo]);
            }
        }

        delete[] bufPool;
        delete[] bufDescTable;
        delete hashTable;
    }


//更新时钟下标位置,注意循环
    void BufMgr::advanceClock()
    {
        clockHand = (clockHand + 1) % (numBufs);
    }


//分配一个空闲帧，并将dirty页写回到磁盘。
    void BufMgr::allocBuf(FrameId & frame)
    {

        FrameId start = clockHand;
        //检查所有帧上页面是否全部固定
        bool unpinned_frame_exists = false;
        while(1) {
            // 更新时钟
            advanceClock();
            BufDesc* curBuf = &bufDescTable[clockHand];

            // 时钟走完一圈检查是否全部固定
            if (clockHand == start) {
                if (!unpinned_frame_exists) throw BufferExceededException();
                else unpinned_frame_exists = false;

            }

            frame = clockHand;
            //找到了没有固定的页面，unpinned_frame_exists设为true
            if(curBuf->pinCnt < 1) unpinned_frame_exists = true;
            //是否是valid
            if(curBuf->valid) {

                //refbit是否为1 -- 如果为1,设为0
                if(curBuf->refbit){
                    curBuf->refbit = 0;
                    continue;
                }
                //是否固定，固定直接下一次循环
                if (curBuf->pinCnt > 0) {
                    continue;
                }

                //dirty 位是否为1 --如果为1则写回磁盘
                if(curBuf->dirty)
                {
                    curBuf->file->writePage(bufPool[clockHand]);
                }
                hashTable->remove(curBuf->file, curBuf->pageNo);
                curBuf->Clear();
                return;


            }
            else {
                //如果无效，直接选择该帧
                frame = clockHand;
                curBuf->Clear();
                return;
            }



        }

    }

/**
* 读页面，如果page不在缓冲池则将页面加载到缓冲池，需要文件指针，page编号，page指针
*/
    void BufMgr::readPage(File* file, const PageId pageNo, Page*& page)
    {
        //记录该page所在帧位置
        FrameId frameNo;
        try{
            // //通过哈希表找page位置
            hashTable->lookup(file, pageNo, frameNo);
        }
        catch(HashNotFoundException) {
            //不在哈希表中, 找空闲帧放入该page
            allocBuf(frameNo);
            bufPool[frameNo] = file->readPage(pageNo);
            hashTable->insert(file, pageNo, frameNo);

            BufDesc* buf = &bufDescTable[frameNo];

            buf->Set(file, pageNo);
            page = &bufPool[frameNo];
            return;
        }
        // 如果page在bufpool里，pincnt++，refbit设为1
        BufDesc* buf = &bufDescTable[frameNo];
        buf->refbit = 1;
        buf->pinCnt++;
        page = &bufPool[frameNo];
    }


/**
减少某页面的pincnt，更新dirty
*/
    void BufMgr::unPinPage(File* file, const PageId pageNo, const bool dirty)
    {
        FrameId frameNo;
        try {
            // 在哈希表中寻找该page
            hashTable->lookup(file, pageNo, frameNo);
        }
        catch(HashNotFoundException) {
            return;
        }

        BufDesc* buf = &bufDescTable[frameNo];
        //检查dirty位，设置dirty位
        if(dirty == true) {buf->dirty = true;}
        // 此时页面应该已经固定pinned
        if(buf->pinCnt < 1) {
            throw PageNotPinnedException("filename", pageNo, frameNo);
        }
        // Pincnt--
        buf->pinCnt--;
    }


/**
寻找某个空的页面，加载到缓冲池
*/
    void BufMgr::allocPage(File* file, PageId &pageNo, Page*& page)
    {
        FrameId frameNo;


        //找到某个空闲帧
        allocBuf(frameNo);
        //找到某个可以写回的页面
        bufPool[frameNo] = file->allocatePage();
        pageNo = bufPool[frameNo].page_number();
        //更新缓冲池
        page = &bufPool[frameNo];
//更新哈希表记录,更新该帧状态
        hashTable->insert(file, bufPool[frameNo].page_number(), frameNo);
        bufDescTable[frameNo].Set(file,bufPool[frameNo].page_number());



    }


/**
将所有关于该file的dirty页面写回磁盘并清空对应缓存
*/
    void BufMgr::flushFile(const File* file)
    {
        //check each frame to find a file and page
        for(unsigned int i = 0; i < numBufs ; i++)
        {

            BufDesc* desc = &bufDescTable[i];
            //找到属于该文件的帧
            if(desc->file == file)
            {
                // 此时该帧应该有效
                if(!desc->valid)
                    throw BadBufferException(desc->frameNo, desc->dirty, desc->valid, desc->refbit);
                //此时应该没有被固定
                if(desc->pinCnt)
                    throw PagePinnedException("filename", desc->pageNo, desc->frameNo);
                //dirty页写回磁盘
                if(desc->dirty == 1)
                {
                    desc->file->writePage(bufPool[desc->frameNo]);
                    desc->dirty = 0;
                }
                //更新哈希表
                hashTable->remove(desc->file, desc->pageNo);
                //释放该帧
                desc->Clear();

            }
        }
    }


/**
删除某文件的某一个page
*/
    void BufMgr::disposePage(File* file, const PageId PageNo)
    {
        //查看哈希表找到该page位置
        for (unsigned i = 0; i < numBufs; i++) {
            BufDesc* buf = &bufDescTable[i];
            if(buf->file == file && buf->pageNo == PageNo){
                //清除对应哈希表数据
                hashTable->remove(buf->file, buf->pageNo);
                // 清空该帧
                buf->Clear();
            }
        }
        // 文件中清除该page
        file->deletePage(PageNo);
    }
//输出缓冲区信息
    void BufMgr::printSelf(void)
    {
        BufDesc* tmpbuf;
        int validFrames = 0;

        for (std::uint32_t i = 0; i < numBufs; i++)
        {
            tmpbuf = &(bufDescTable[i]);
            std::cout << "FrameNo:" << i << " ";
            tmpbuf->Print();

            if (tmpbuf->valid == true)
                validFrames++;
        }

        std::cout << "Total Number of Valid Frames:" << validFrames << "\n";
    }

}
