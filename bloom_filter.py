import hashlib

class BitArray:
	def __init__(self, bits):
		self._arr = [ False ] * bits
	def __iter__(self):
		return iter(self._arr)
	def __getitem__(self, index):
		return self._arr[index]
	def __setitem__(self, index, item):
		if item:
			self._arr[index] = True
		else:
			self_.arr[index] = False

class BloomFilter:
	def __init__(self, bits):
		self._filter = BitArray(bits)
		self._bits = bits
	def _keys(self, item):
		k1 = hashlib.sha1(item.encode()).hexdigest()
		k2 = hashlib.md5(item.encode()).hexdigest()
		k3 = hashlib.sha256(item.encode()).hexdigest()
		return { int(k, 16) % self._bits for k in (k1, k2, k3) }
	def insert(self, item):
		for key in self._keys(item):
			self._filter[key] = True
	def lookup(self, item):
		for key in self._keys(item):
			if not self._filter[key]:
				return False
		return True
