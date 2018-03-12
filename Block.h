#ifndef BLOCK_H
#define BLOCK_H

#include <cstdint>
#include <iostream>
#include <time.h>
using namespace std;

class Block {
public:
	string sPrevHash;

	Block(uint32_t nIndexIn, const string &sDataIn);
	Block(uint32_t nIndexIn, const string &sDataIn, const string &sPHash, const string &sHash);

	string GetHash();
	string GetData();

	string toString();
	
	void MineBlock(uint32_t nDifficulty);

private:
	uint32_t _nIndex;
	int64_t _nNonce;
	string _sData;
	string _sHash;
	time_t _tTime;

	string _CalculateHash() const;
};

#endif