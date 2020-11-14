/**
 * @author Zhaonian Zou <znzou@hit.edu.cn>,
 * School of Computer Science and Technology,
 * Harbin Institute of Technology, China
 */

#include "schema.h"

#include <string>
#include <iostream>
#include <sstream>
using namespace std;

namespace badgerdb
{
    void split(const string& s,vector<string>& sv,const char flag = ' ') {
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
//根据sql语言建表模式
    TableSchema TableSchema::fromSQLStatement(const string &sql)
    {
        string tableName; //表名
        vector<Attribute> attrs; //属性集合
        bool isTemp = false;
        std::string::size_type nPos1 ;
        std::string::size_type nPos2 ;
        std::string::size_type nPos4 ;
        nPos1 =sql.find("(");
        nPos2 =sql.find_last_of(")");
        nPos4 =sql.find("TABLE");
        tableName=sql.substr(nPos4+6,nPos1-nPos4-7);//提取表名
        string a=sql.substr(nPos1+1,nPos2-nPos1-1);//提取属性描述
        vector<string> sv;
//split为手写分割函数，通过分割符号返回字符串容器
        split(a, sv, ',');//分割不同属性描述
        for (const auto& s : sv) {
//      cout<<s<<endl;
            vector<string> sv1;
            split(s, sv1, ' ');//分割同一属性描述
            int i=0;
            string q1;
            DataType q2;
            string q;
            int max=4;
            bool q3= false;
            bool q4= false;
            for (const auto& t : sv1){
                if(i==0){
                    q1=t;//属性名称
                    i++;
                    continue;
                }
                    //提取属性的maxsize，以及属性类型
                else if(i==1){
                    std::string::size_type u;
                    u=t.find("(");
                    if(u!=-1){
                        q=t.substr(0,u);
                        max=stoi(t.substr(u+1,t.size()-u));//maxsize
                    }
                    else{
                        q=t;
                    }
                    if(q=="INT"){
                        q2=INT;
                    }
                    if(q=="CHAR"){
                        q2=CHAR;
//                  cout<<q2<<endl;
                    }
                    if(q=="VARCHAR"){
                        q2=VARCHAR;
                    }

                    i++;
                }
                    //提取属性特点
                else if(t=="UNIQUE") {
                    q3 = true;
                }
                else if(t=="NOT"){
                    q4= true;
                }
            }
            //更新attrs
            Attribute *m=new Attribute(q1,q2,max,q3,q4);
            attrs.push_back(*m);
        }
        return TableSchema(tableName, attrs, isTemp);

    }

//输出表的模式信息
    void TableSchema::print() const
    {
        std::cout<<"TableName:"<<getTableName()<<endl;
        int i;
        string  as[3]={"INT","CHAR","VARCHAR"};
        for(i=0;i<getAttrCount();i++){
            std::cout<<attrs[i].attrName<<'|'<<as[attrs[i].attrType]<<'('<<attrs[i].maxSize<<')';
            if(attrs[i].isNotNull){
                cout<<'|'<<"NOT NULL";
            }
            if(attrs[i].isUnique){
                cout<<'|'<<"UNIQUE";
            }
            cout<<endl;

        }

    }

} // namespace badgerdb