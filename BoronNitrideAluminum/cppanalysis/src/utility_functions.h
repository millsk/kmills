#include <string>
#include <vector>
#include <stdio.h>
#include <string.h>

using namespace std;

vector<string> string_split_to_vector(string si) {
  vector<string> sv;
  char * pch;
  char *dup = strdup(si.c_str());
  pch = strtok (dup," ,.-");
  while (pch != NULL)
  {
    sv.push_back(strtok (NULL, " ,.-"));
  }
  return sv;



}


