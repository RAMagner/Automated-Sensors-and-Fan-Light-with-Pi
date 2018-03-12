#ifndef BLOCKCHAIN_H
#define BLOCKCHAIN_H

#include <vector>
#include "Block.h"

using namespace std;

class BlockChain
{
public:
	BlockChain();
	BlockChain(vector<Block> bOld);
	void AddBlock(Block bNew);
	void PrintChain();
private:
	uint32_t		_nDifficulty = 3;
	vector<Block>	_vChain;

	Block _GetLastBlock();
};

#endif