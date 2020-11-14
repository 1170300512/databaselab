/**
 * @author Zhaonian Zou <znzou@hit.edu.cn>,
 * School of Computer Science and Technology,
 * Harbin Institute of Technology, China
 */

#include "storage.h"
#include "file_iterator.h"
#include "page_iterator.h"
#include <iostream>
#include <string>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <sstream>
#include "exceptions/insufficient_space_exception.h"
#include "exceptions/page_not_pinned_exception.h"

using namespace std;

namespace badgerdb
{
    static void split(const string& s,vector<string>& sv,const char flag = ' ') {
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
    RecordId HeapFileManager::insertTuple(const string &tuple, File &file, BufMgr *bufMgr)
    {
        Page p;
        PageId pageId;
        Page* page;
        bool find= false;
        RecordId recordId;
//先在file里找不满的page，找到后用buffpool读取，如果内存中该page已经满了，就写回，加载一块新page写，不满就直接写回
        for (FileIterator iter = file.begin();iter != file.end();++iter) {
            p = *iter;
            pageId++;
            if(p.hasSpaceForRecord(tuple)){
                find= true;
                break;
            }
        }

        if(find){
            bufMgr->readPage(&file,p.page_number(),page);

            if(page->hasSpaceForRecord(tuple)){
                recordId=page->insertRecord(tuple);

            } else{
                bufMgr->allocPage(&file,pageId,page);
                page->insertRecord(tuple);
            }
        } else{
            bufMgr->allocPage(&file,pageId,page);
            page->insertRecord(tuple);
        }
        bufMgr->unPinPage(&file,page->page_number(),1);
        file.writePage(*page);
//    cout<<page->page_number()<<endl;
        return recordId;


    }

    void HeapFileManager::deleteTuple(const RecordId &rid, File &file, BufMgr *bufMgr)
    {
        PageId  pageId=rid.page_number;
        Page* page1;
        bufMgr->readPage(&file,pageId,page1);
        page1->deleteRecord(rid);
        file.writePage(*page1);

    }

//创建元组，根据sql语句
    string HeapFileManager::createTupleFromSQLStatement(const string &sql, const Catalog *catalog)
    {
        string tablename;
        std::string::size_type nPos1 ;
        std::string::size_type nPos2 ;
        std::string::size_type nPos3 ;
        std::string::size_type nPos4 ;
        nPos1 =sql.find("INTO");
        nPos2 =sql.find("VALUES");
        nPos3 =sql.find("(");
        nPos4=sql.find_last_of(")");
        tablename=sql.substr(nPos1+5,nPos2-nPos1-6);
        string a=sql.substr(nPos3+1,nPos4-nPos3-1);
        vector<string> sv;
        split(a, sv, ',');
        int k=sv.size();
        int i;
        TableId tableid=catalog->getTableId(tablename);
        TableSchema tableSchema=catalog->getTableSchema(tableid);
        string s;
        for(i=0;i<k;i++) {
            if (i>0){
                s.append(" ");//加空格
            }
            string q;
            q=sv[i];
            if (sv[i][0] == ' ') {
                sv[i] = sv[i].substr(1, sv[i].size() - 1);
                q = sv[i];
            }
            if (sv[i][0] == '\'' && sv[i][sv[i].size() - 1] == '\'') {
                q = sv[i].substr(1, sv[i].size() - 2);//去除引号
            }
            DataType dataType = tableSchema.getAttrType(i);
            int o = tableSchema.getAttrMaxSize(i);
            if(dataType==INT){
                s.append(q);
            }
            if(dataType==CHAR){
                q.resize(o);
                s.append(q);

            }
            if(dataType==VARCHAR){
                s.append(q);
            }


        }
//    cout<<s<<endl;
//以a b c ...形式返回
        return s;

    }
} // namespace badgerdb