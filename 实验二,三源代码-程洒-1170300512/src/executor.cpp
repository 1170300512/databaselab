/**
 * @author Zhaonian Zou <znzou@hit.edu.cn>,
 * School of Computer Science and Technology,
 * Harbin Institute of Technology, China
 */

#include "executor.h"

#include <functional>
#include <string>
#include <iostream>
#include <ctime>

#include "storage.h"
#include "file_iterator.h"
#include "page_iterator.h"
#include <iomanip>
#include <sstream>
#include <cstring>
#include <cmath>

using namespace std;

namespace badgerdb
{    static void split(const string& s,vector<string>& sv,const char flag = ' ') {
        sv.clear();
        istringstream iss(s);
        string temp;

        while (getline(iss, temp, flag)) {
            if(!temp.empty()) {
                sv.push_back(temp);
            }
        }
        return;
    }


//打印表及其元组信息
    void TableScanner::print() const
    {
        File file = TableScanner::tableFile;
        bufMgr->flushFile(&tableFile);
        stringstream names;
        stringstream header;
        header << "+";
        names << "|\t";
        for (int i = 0; i < tableSchema.getAttrCount(); i++)
        {
            string atrname = tableSchema.getAttrName(i);
            names << atrname << "\t|\t";
            header << "---------------+";
        }
        tableSchema.print();
        cout << header.str() << endl;
        cout << names.str() << endl;
        cout << header.str() << endl;
        Page p;
        //遍历文件中page
        for (FileIterator iter = (file).begin();iter != file.end();++iter) {

            p=*iter;
            //遍历page中元组
            for (PageIterator page_iter = p.begin();page_iter != p.end();++page_iter) {
                cout<<"|\t";
                string a = (*page_iter);
                vector<string> b;
                split(a, b, ' ');
                for (int j = 0; j < b.size(); ++j) {
                    cout << b[j] << "\t|\t";
                }
                cout<<endl;
            }
        }
    }

bool check(const File &leftTableFile, const File &rightTableFile)
{
    File lf = leftTableFile;
    File rf = rightTableFile;
    int l = 0;
    int r = 0;
    for (FileIterator it = lf.begin(); it != lf.end(); it++)
        l++;
    for (FileIterator it = rf.begin(); it != rf.end(); it++)
        r++;
    return l < r;
}
JoinOperator::JoinOperator(const File &leftTableFile,
                           const File &rightTableFile,
                           const TableSchema &leftTableSchema,
                           const TableSchema &rightTableSchema,
                           Catalog *catalog,
                           BufMgr *bufMgr)
    : leftTableFile(leftTableFile),
      rightTableFile(rightTableFile),
      leftTableSchema(leftTableSchema),
      rightTableSchema(rightTableSchema),
      resultTableSchema(
          createResultTableSchema(leftTableSchema, rightTableSchema)),
      catalog(catalog),
      bufMgr(bufMgr),
      isComplete(false)
{

}
//定义连接后表的模式，默认左表小于右表
    TableSchema JoinOperator::createResultTableSchema(
            const TableSchema &leftTableSchema,
            const TableSchema &rightTableSchema)
    {
        vector<Attribute> attrs;
        // TODO: add attribute definitions
        int  num1=leftTableSchema.getAttrCount();//左表属性数量
        int  num2=rightTableSchema.getAttrCount();//右表属性数量
        //将左表属性全加入结果的属性集合里
        for (int i = 0; i <num1 ; ++i) {
            Attribute attribute(leftTableSchema.getAttrName(i),leftTableSchema.getAttrType(i),leftTableSchema.getAttrMaxSize(i),leftTableSchema.isAttrNotNull(i),leftTableSchema.isAttrUnique(i));
            attrs.push_back(attribute);
        }
        //右表如果有i左表没有的属性就加入
        for (int j = 0; j <num2 ; ++j) {
            if(leftTableSchema.hasAttr(rightTableSchema.getAttrName(j))){
                continue;
            } else{
                Attribute attribute1(rightTableSchema.getAttrName(j),rightTableSchema.getAttrType(j),rightTableSchema.getAttrMaxSize(j),rightTableSchema.isAttrNotNull(j),rightTableSchema.isAttrUnique(j));
                attrs.push_back(attribute1);
            }
        }
        return TableSchema("TEMP_TABLE", attrs, true);
    }

void JoinOperator::printRunningStats() const
{
    cout << "# Result Tuples: " << numResultTuples << endl;
    cout << "# Used Buffer Pages: " << numUsedBufPages << endl;
    cout << "# I/Os: " << numIOs << endl;
}


    //一趟连接算法
    bool OnePassJoinOperator::execute(int numAvailableBufPages, File &resultFile)
    {
        if (isComplete)
            return true;

        numResultTuples = 0;
        numUsedBufPages = 0;
        numIOs = 0;
        Page* page[numAvailableBufPages-1];//存储小表的各个加载到内存的指针
        Page* page1;
        Page* page2;
        // TODO: Execute the join algorithm
        File file1=leftTableFile;
        File file2=rightTableFile;
        Page p;
        TableSchema rtable = rightTableSchema;
        TableSchema ltable = leftTableSchema;
//检测哪个表小,小的设为左表全部加载到内存
        if(!check(file1, file2))
        {
            file2 = leftTableFile;
            file1 = rightTableFile;
            rtable = leftTableSchema;
            ltable = rightTableSchema;
        }
        //加载left表到内存,指针数组记录各个页面
        for (FileIterator iter = (file1).begin();iter != file1.end();++iter) {
            p=*iter;
            bufMgr->readPage(&file1,p.page_number(),page[numUsedBufPages]);
            numUsedBufPages++;//更新使用内存数
            numIOs++;//更新IO数
        }
//遍历right表的所有page
        for (FileIterator iter1 = (file2).begin();iter1 != file2.end();++iter1) {
            p=*iter1;
            bufMgr->readPage(&file2,p.page_number(),page1);
            numIOs++;//更新IO数
//遍历page的所有元组
            for (PageIterator page_iter2 = p.begin();page_iter2 != p.end();++page_iter2) {
                string a = (*page_iter2);//获取一条元组
                vector<string> b;
                split(a, b, ' ');//切分元组
//通过指针遍历buffpool中left表中所有page
                for(int i=0;i<numUsedBufPages;i++){
                    Page p1=*page[i];
//遍历frame中所有元组
                    for (PageIterator page_iter3 = p1.begin();page_iter3 != p1.end();++page_iter3) {
                        string c = (*page_iter3);
                        vector<string> d;
                        split(c, d, ' ');//切分元组
                        string m;//记录新的元组
                        int j=0;
//遍历连接后的表属性信息
                        for(j=0;j<resultTableSchema.getAttrCount();j++){
                            if(j!=0){
                                m.append(" ");
                            }
//查看共同属性是否相等
                            if(ltable.hasAttr(resultTableSchema.getAttrName(j))&&rtable.hasAttr(resultTableSchema.getAttrName(j))){
                                int po1=ltable.getAttrNum(resultTableSchema.getAttrName(j));
                                int po2=rtable.getAttrNum(resultTableSchema.getAttrName(j));
                                string s1=d[po1];
                                string s2=b[po2];
                                if(s1==s2){
                                    m.append(s1);
                                } else{
                                    break;
                                }
                            }
//非共同属性左表赋值
                            else if(ltable.hasAttr(resultTableSchema.getAttrName(j))){
                                int po1=ltable.getAttrNum(resultTableSchema.getAttrName(j));
                                string s1=d[po1];
                                m.append(s1);
                            }

//非共同属性右表赋值

                            else if(rtable.hasAttr(resultTableSchema.getAttrName(j))){
                                int po2=rtable.getAttrNum(resultTableSchema.getAttrName(j));
                                string s2=b[po2];
                                m.append(s2);
                            }
                        }
//结果表属性遍历完成,元组匹配成功,插入元组
                        if(j==resultTableSchema.getAttrCount()){
                            HeapFileManager::insertTuple(m,resultFile,bufMgr);
                            numResultTuples++;
                        }
                    }
                }
            }
//释放该帧
            bufMgr->unPinPage(&file2,p.page_number(),0);
        }
        bufMgr->clearBufStats();
        numUsedBufPages++;

        isComplete = true;
        return true;
    }

bool NestedLoopJoinOperator::execute(int numAvailableBufPages, File &resultFile)
{
        if (isComplete)
            return true;

        numResultTuples = 0;
        numUsedBufPages = 0;
        numIOs = 0;
    Page* page[numAvailableBufPages-1];//存储小表的各个加载到内存的指针
        Page* page1;
        Page* page2;

        // TODO: Execute the join algorithm
        File file1=leftTableFile;
        File file2=rightTableFile;
        Page p;
        TableSchema rtable = rightTableSchema;
        TableSchema ltable = leftTableSchema;
    vector<string> b;
    vector<string> d;
//检测哪个表小,小的设为左表全部加载到内存
        if(!check(file1, file2))
        {
            file2 = leftTableFile;
            file1 = rightTableFile;
            rtable = leftTableSchema;
            ltable = rightTableSchema;
        }
        //加载left表到内存,指针数组记录各个页面
        int i=0;
        FileIterator it = file1.begin();
    while (it != file1.end())
    {

        int i=0;
        for (i = 0; i < numAvailableBufPages-1 && it != file1.end(); it++)
        {
            p=*it;

            bufMgr->readPage(&file1,p.page_number(),page[i]);
            numUsedBufPages++;//更新使用内存数
            numIOs++;//更新IO数
            i++;
        }
//遍历right表的所有page
            for (FileIterator iter1 = (file2).begin(); iter1 != file2.end(); ++iter1) {
                p = *iter1;
                bufMgr->readPage(&file2, p.page_number(), page1);
                numIOs++;//更新IO数
//遍历page的所有元组

                for (PageIterator page_iter2 = p.begin(); page_iter2 != p.end(); ++page_iter2) {
                    string a = (*page_iter2);//获取一条元组

                    split(a, b, ' ');//切分元组
//通过指针遍历buffpool中left表中所有page
                    for (int k = 0; k < i; k++) {
                        Page p1 = *page[k];
//遍历frame中所有元组

                        for (PageIterator page_iter3 = p1.begin(); page_iter3 != p1.end(); ++page_iter3) {
                            string c = (*page_iter3);

                            split(c, d, ' ');//切分元组
                            string m;//记录新的元组
                            int j = 0;
//遍历连接后的表属性信息
                            for (j = 0; j < resultTableSchema.getAttrCount(); j++) {
                                if (j != 0) {
                                    m.append(" ");
                                }
//查看共同属性是否相等
                                if (ltable.hasAttr(resultTableSchema.getAttrName(j)) &&
                                    rtable.hasAttr(resultTableSchema.getAttrName(j))) {
                                    int po1 = ltable.getAttrNum(resultTableSchema.getAttrName(j));
                                    int po2 = rtable.getAttrNum(resultTableSchema.getAttrName(j));
                                    string s1 = d[po1];
                                    string s2 = b[po2];
                                    if (s1 == s2) {
                                        m.append(s1);
                                    } else {
                                        break;
                                    }
                                }
//非共同属性左表赋值
                                else if (ltable.hasAttr(resultTableSchema.getAttrName(j))) {
                                    int po1 = ltable.getAttrNum(resultTableSchema.getAttrName(j));
                                    string s1 = d[po1];
                                    m.append(s1);
                                }

//非共同属性右表赋值

                                else if (rtable.hasAttr(resultTableSchema.getAttrName(j))) {
                                    int po2 = rtable.getAttrNum(resultTableSchema.getAttrName(j));
                                    string s2 = b[po2];
                                    m.append(s2);
                                }
                            }
//结果表属性遍历完成,元组匹配成功,插入元组
                            if (j == resultTableSchema.getAttrCount()) {
                                HeapFileManager::insertTuple(m, resultFile, bufMgr);
                                numResultTuples++;
                            }
                            d.clear();
                        }
                    }
                    b.clear();
                }
//释放该帧
                bufMgr->unPinPage(&file2, p.page_number(), 0);

            }
        bufMgr->clearBufStats();
        }
        numUsedBufPages++;
        isComplete = true;
        return true;

}

BucketId GraceHashJoinOperator::hash(const string &key) const
{
    std::hash<string> strHash;
    return strHash(key) % numBuckets;
}

bool GraceHashJoinOperator ::execute(int numAvailableBufPages, File &resultFile)
{
    if (isComplete)
        return true;

    numResultTuples = 0;
    numUsedBufPages = 0;
    numIOs = 0;

    // TODO: Execute the join algorithm

    isComplete = true;
    return true;
}

} // namespace badgerdb