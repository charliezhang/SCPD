function tmp = q2_main()
  G = load('q2-data/graph.txt');
  degs = zeros(100, 1);
  M = zeros(100, 100);
  for i=1:size(G, 1)
    degs(G(i,1)) = degs(G(i,1)) + 1;
  end
  for k=1:size(G, 1)
    i = G(k,1);
    j = G(k,2);
    M(j, i) = 1 / degs(i);
  end
  
  beta = 0.2;
  
  tic
  PI(40, M, beta)
  toc
  
end

function r = PI(iter, M, beta)
  n = size(M, 1);
  one = ones(n, 1) / n;
  r = one;
  for i=1:iter
    r = (1 - beta) / n * one + beta * M * r;
  end
end

function r = MC(iter, M, beta, R)
  n = size(M, 1);
  
end