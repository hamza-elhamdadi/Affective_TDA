#include <iostream>
#include <string>
#include <map>
#include <sstream>
#include <vector>
#include <fstream>

int main()
{
    std::ifstream file("Data/test.csv");
    if(!file){
        std::cout << "File failed to open" << std::endl;
    }

    std::string first_line, key_line;

    getline(file, first_line);
    getline(file, key_line);

    std::string curr;
    std::vector<std::string> first_arr, key;
    std::stringstream first(first_line), keystream(key_line);

    while(getline(first, curr, ','))
    {
        first_arr.push_back(curr);
    }

    while(getline(keystream, curr, ','))
    {
        key.push_back(curr);
    }



    //std::map<std::string, std::vector<>>;
    return 0;
}