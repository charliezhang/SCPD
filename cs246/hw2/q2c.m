function ans = q2c()
  D = load('Matrix.txt');
  r(D)
  [U, S, V] = svd(D, 'econ');
  K = [];
  R = [];
  for k=197:50:497
    Sk = trim(S, k);
    Dk = U * Sk * V';
    K = [K; k]
    R = [R; r(Dk)]
  end
  plot(K, R)
end

function ans = r(D)
  k = 100;
  n = size(D, 1);
  ans = sum_cossim(D(1:k, :)) / nchoosek(k, 2) / sum_cossim(D) * nchoosek(n, 2);
end

function ans = sum_cossim(D)
  ans = 0;
  n = size(D, 1);
  for i=1:n-1
    for j=i+1:n
      ans = ans + cossim(D(i,:), D(j,:));
    end
  end
end

function ans = cossim(u, v)
  ans = u * v' / sqrt(u * u') / sqrt(v * v');
end

function ans = trim(S, k)
  n = min(size(S, 1), size(S, 2));
  ans = S;
  for i=k+1:n
    ans(i,i) = 0;
  end
end