function r = main()
  R = load('q1-data/user-shows.txt');
  m = size(R, 1);
  n = size(R, 2);
  P = zeros(m, m);
  Q = zeros(n, n);
  for i=1:m
    P(i,i) = sum(R(i,:));
  end
  for i=1:n
    Q(i,i) = sum(R(:,i));
  end

  
  idx_alex = 500;
  Su = P^(-1/2)*R*R'*P^(-1/2);
  GammaUU = Su * R;
  [topUU, top_idxUU] = sort(GammaUU(idx_alex, 1:100), 'descend');
  topUU
  top_idxUU
  alex = load('q1-data/alex.txt');
  plot_precision(top_idxUU, alex)


  Si = Q^(-1/2)*R'*R*Q^(-1/2);
  GammaII = R * Si;
  [topII, top_idxII] = sort(GammaII(idx_alex, 1:100), 'descend');
  topII
  top_idxII
  plot_precision(top_idxII, alex)
end

function x = plot_precision(top_idx, alex)
  results = [];
  for k = 1:19
    score = 0;
    for i = 1:k
      score = score + alex(top_idx(i));
    end
    score = score / k;
    results = [results; k, score];
  end
  plot(results(:,1), results(:,2))
end
