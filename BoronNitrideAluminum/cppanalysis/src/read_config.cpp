#include <fstream>
#include <string>
#include "yaml-cpp/yaml.h"
#include <iostream>
#include "utility_functions.h"
#include "data_structure.h"

using namespace std;
using namespace YAML;

template<class T>
static void parse(const Node& node, const char* key, T& value) {
    if (node.FindValue(key)) {
        node[key] >> value;
    } else {
        printf("CONFIG: '%s' was not found!\n", key);
    }
}


void parse_inputfile(Configuration& config, const Node& node) {
    const Node& plots = node["plots"];
    parse(plots, "msd", config.msd);
    parse(plots, "msd_outputfilename", config.msd_outputfilename);
    parse(plots, "msd_atoms", config.tempstr);
      config.msd_atoms = str2vec(config.tempstr);
    
}




bool read_configfile(Configuration& config) {
    fstream file("config.yaml", fstream::in);
    if (!file.is_open()) {
        return false;
    }
    Parser parser(file);
    Node root;
    parser.GetNextDocument(root);
    parse_inputfile(config, root);
    cout << "Configuration file \"config.yaml\" read.\n\n";
    return true;
}
