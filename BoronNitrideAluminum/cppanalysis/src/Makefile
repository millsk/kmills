

main: readXML.cpp data_structure.h  
	$(CXX) -std=c++11 main.cpp tinyxml/tinyxml.cpp tinyxml/tinyxmlerror.cpp tinyxml/tinyxmlparser.cpp tinyxml/tinystr.cpp -Ltinyxml/ -Lyaml-cpp/ -lyaml-cpp -oreadXML

clang: readXML.cpp data_structure.h  
	clang++ -std=c++11 main.cpp tinyxml/tinyxml.cpp tinyxml/tinyxmlerror.cpp tinyxml/tinyxmlparser.cpp tinyxml/tinystr.cpp -Ltinyxml/ -Lyaml-cpp/ -lyaml-cpp -oreadXML

clean:
	rm readXML



