#include "BlockChain.h"
#include <iostream>
#include <fstream>
#include <string>


BlockChain::BlockChain()
{
	Block bNew(0, "Genesis Block");
	bNew.sPrevHash = "null";
	bNew.MineBlock(_nDifficulty);
	_vChain.emplace_back(bNew);
}

BlockChain::BlockChain(vector<Block> bOld) {
	uint32_t i = 0;
	for(auto b : bOld) {
		if(i == 0)
			_vChain.emplace_back(b);
		else
			_vChain.push_back(b);

		if (i + 1 != 0)
			i++;
	}
}

void BlockChain::AddBlock(Block bNew)
{
	bNew.sPrevHash = _GetLastBlock().GetHash();
	bNew.MineBlock(_nDifficulty);
	_vChain.push_back(bNew);

	std::ofstream file("blockchain.txt");
	for(auto b : _vChain)
		file << b.toString();
	file.close();
}

void BlockChain::PrintChain()
{
	for(auto b : _vChain) {
		std::cout << b.toString();
	}
}


Block BlockChain::_GetLastBlock()
{
	return _vChain.back();
}
