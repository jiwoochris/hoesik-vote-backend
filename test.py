def count_divisible_subarrays(A, K):
	"""
	배열 A의 연속 부분배열 중 모든 원소를 곱한 값이 K의 배수인 부분배열의 개수를 반환
	
	Args:
		A: 정수 배열
		K: 양의 정수
	
	Returns:
		K의 배수가 되는 부분배열의 총 개수
	"""
	from collections import defaultdict
	
	def prime_factorize(n):
		"""정수 n의 소인수분해 결과를 딕셔너리로 반환"""
		factors = defaultdict(int)
		d = 2
		while d * d <= n:
			while n % d == 0:
				factors[d] += 1
				n //= d
			d += 1
		if n > 1:
			factors[n] += 1
		return factors
	
	def is_divisible_by_k(product_factors, k_factors):
		"""product_factors가 k_factors로 나누어떨어지는지 확인"""
		for prime, required_count in k_factors.items():
			if product_factors.get(prime, 0) < required_count:
				return False
		return True
	
	# K의 소인수분해
	k_factors = prime_factorize(K)
	
	# 각 원소의 소인수분해 미리 계산
	element_factors = [prime_factorize(num) for num in A]
	
	count = 0
	n = len(A)
	
	# 모든 부분배열 [l, r]에 대해 검사
	for l in range(n):
		current_factors = defaultdict(int)
		
		for r in range(l, n):
			# A[r]의 소인수들을 현재 곱에 추가
			for prime, exp in element_factors[r].items():
				current_factors[prime] += exp
			
			# 현재 부분배열의 곱이 K의 배수인지 확인
			if is_divisible_by_k(current_factors, k_factors):
				count += 1
	
	return count


def test_count_divisible_subarrays():
	"""
	배수 부분배열 세기 함수의 테스트 케이스
	"""
	# Given: 첫 번째 예시 - A=[3,1,2,2,3], K=6
	A1 = [3, 1, 2, 2, 3]
	K1 = 6
	
	# When: count_divisible_subarrays 함수를 호출한다
	result1 = count_divisible_subarrays(A1, K1)
	
	# Then: 6개의 부분배열이 K의 배수여야 한다
	assert result1 == 6
	
	# Given: 두 번째 예시 - A=[1,2,3], K=7
	A2 = [1, 2, 3]
	K2 = 7
	
	# When: count_divisible_subarrays 함수를 호출한다
	result2 = count_divisible_subarrays(A2, K2)
	
	# Then: 0개의 부분배열이 K의 배수여야 한다
	assert result2 == 0
	
	# Given: 단일 원소 배열 - A=[6], K=6
	A3 = [6]
	K3 = 6
	
	# When: count_divisible_subarrays 함수를 호출한다
	result3 = count_divisible_subarrays(A3, K3)
	
	# Then: 1개의 부분배열이 K의 배수여야 한다
	assert result3 == 1
	
	# Given: 모든 원소가 1인 배열 - A=[1,1,1], K=1
	A4 = [1, 1, 1]
	K4 = 1
	
	# When: count_divisible_subarrays 함수를 호출한다
	result4 = count_divisible_subarrays(A4, K4)
	
	# Then: 모든 부분배열(6개)이 K의 배수여야 한다
	assert result4 == 6  # 3*(3+1)//2 = 6


if __name__ == "__main__":
	test_count_divisible_subarrays()
	print("모든 테스트가 통과했습니다!")