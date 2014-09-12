#include <fstream>
#include <iostream>
#include <stdio.h>
#include "data_structure.h"
#include "tinyxml/tinyxml.h"
#include "tinyxml/tinystr.h"
//#define TIXML_USE_STL
using namespace std;





//int readXML(FileInfo& info) {
int readXML() {
   TiXmlDocument doc;
//   if (doc.LoadFile(info.input_filename.c_str())) {
   if (!doc.LoadFile("vasprun.xml")) {
      cerr << doc.ErrorDesc() << endl;
      return 0;
   }
  

  for(TiXmlElement* elem = doc.FirstChildElement(); elem != NULL; elem = elem->NextSiblingElement())
  {
     string elemName = elem->Value();
     cout << elemName << endl;
  }
  
   

}


int main() {
   cout << "\n Starting XML read"<<endl;
   readXML();
   cout << "\n done"<<endl;
}





   

















