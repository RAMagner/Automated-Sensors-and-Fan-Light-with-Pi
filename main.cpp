#include "BlockChain.h"
#include "Block.h"
#include <iostream>
#include <string>
#include <sstream>
#include <fstream>

int main(int argc, char *argv[])
{
	vector<Block> vChain;
	string index, prevHash, sHash, sData = "";
	int iIndex = 0;
	BlockChain bChain;
	Block bOld(0, "");
	if (argc == 2)
	{
		std::ifstream infile(argv[1]);
		std::string line;

		while (std::getline(infile, line))
		{
			std::stringstream ss(line);
			std::string data;
			ss >> index;
			ss >> prevHash;
			ss >> sHash;
			while(ss >> data) {
				sData = sData + " " + data;
			}
			bOld = Block(atoi(index.c_str()), sData, prevHash, sHash);
			vChain.push_back(bOld);
			sData = "";
			iIndex++;
		}
		bChain = BlockChain(vChain);
	}

	cout << "Mining block 1..." << endl;
	bChain.AddBlock(Block(++iIndex, ("Block " + to_string(iIndex) + " Data")));

	cout << "Mining block 2..." << endl;
	bChain.AddBlock(Block(++iIndex, ("Block " + to_string(iIndex) + " Data")));

	cout << "Mining block 3..." << endl;
	bChain.AddBlock(Block(++iIndex, ("Block " + to_string(iIndex) + " Data")));

	bChain.PrintChain();

	return 0;
}