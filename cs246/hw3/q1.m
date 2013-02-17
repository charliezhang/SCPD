function tmp = q1_main()

  train_set = 'q1-data/ratings.train.txt';
  test_set = 'q1-data/ratings.val.txt';
  % Store R in memory only to accelerate program execution.
  % Algorithm and code logic rename same as R is read from file.
  [Rtrain, max_m, max_n, all_i, all_u] = init(train_set);
  [Rtest, tmp1, tmp2, tmp3, tmp4] = init(test_set);

  [v_i, v_u, v_r] = find(Rtest);
  for j = 1:size(v_u)
    u = v_u(j);
    i = v_i(j);
    if i > max_m || all_i(i) == 0 || u > max_n || all_u(u) == 0
      Rtest(i,u) = 0;
      fprintf('Not fould (%d, %d) in training set. setting test val to zero.\n', i, u)
    end
  end
  
  
 %{
 for eta = 0.002:0.002:0.02
  k = 20;
  I = 40;
  lambda = 0.2;
  eta = 0.002;
  scalar = sqrt(5 / k);
  Q = rand(max_m, k, 'double') * scalar;
  P = rand(max_n, k, 'double') * scalar;
  E = [];
  for i=1:I
    [Q, P] = SGD(Rtrain, Q, P, k, lambda, eta);
    e = error(Rtrain, Q, P, lambda)
    E = [E; e];
  end
  figure;
  plot(E)
  title(sprintf('n = %.3f', eta));
  xlabel('Num of iterations');
  ylabel('Error');
end

  
  I = 40;
  eta = 0.03;
  lambda = 0.0;
  E_tr = [];
  E_te = [];
  for kk = 1:10
    [e1, e2] = train_and_eval(Rtrain, Rtest, max_m, max_n, kk, I, lambda, eta);
    e1
    e2
    E_tr = [E_tr; e1];
    E_te = [E_te; e2];
  end
  figure;
  plot(E_te)
  title(sprintf('Test error with lambda = %f', lambda));
  xlabel('K');
  ylabel('Error');
  
  figure;
  plot(E_tr)
  title(sprintf('Train error with lambda = %f', lambda));
  xlabel('K');
  ylabel('Error');

  
  I = 40;
  eta = 0.03;
  lambda = 0.2;
  E_tr = [];
  E_te = [];
  for kk = 1:10
    [e1, e2] = train_and_eval(Rtrain, Rtest, max_m, max_n, kk, I, lambda, eta);
    E_tr = [E_tr; e1];
    E_te = [E_te; e2];
  end
  figure;
  plot(E_te)
  title(sprintf('Test error with lambda = %f', lambda));
  xlabel('K');
  ylabel('Error');
  
  figure;
  plot(E_tr)
  title(sprintf('Train error with lambda = %f', lambda));
  xlabel('K');
  ylabel('Error');

    %}   
  
  k = 10;
  I = 40;
  lambda = 0.2;
  eta = 0.03;
  scalar = sqrt(5 / k);
  Q = rand(max_m, k, 'double') * scalar;
  P = rand(max_n, k, 'double') * scalar;
  b_i = zeros(max_m, 1);
  sum_i = zeros(max_m, 1);
  b_u = zeros(max_n, 1);
  sum_u = zeros(max_n, 1);
  cnt = 0;
  sum = 0;
  [v_i, v_u, v_r] = find(Rtest);
  for j = 1:size(v_u)
    u = v_u(j);
    i = v_i(j);
    R_iu = v_r(j);
    b_i(i) = b_i(i) + R_iu;
    sum_i(i) = sum_i(i) + 1;
    b_u(u) = b_u(u) + R_iu;
    sum_u(u) = sum_u(u) + 1;
    cnt = cnt + 1;
    sum = sum + R_iu;
  end
  mu = sum / cnt;
  for i=1:max_m
    if sum_i(i) > 0
      b_i(i) = b_i(i) ./ sum_i(i) - mu;
    else
      b_i(i) = 0;
    end
  end
  for i=1:max_n
    if sum_u(i) > 0
      b_u(i) = b_u(i) ./ sum_u(i) - mu;
    else
      b_u(i) = 0;
    end
  end
  E = [];
  for i=1:I
    [Q, P, b_u, b_i] = SGD2(Rtrain, Q, P, mu, b_u, b_i, k, lambda, eta);
    e = error2(Rtrain, Q, P, mu, b_u, b_i, lambda);
    E = [E; e];
  end
  figure;
  plot(E)
  title(sprintf('n = %.3f', eta));
  xlabel('Num of iterations');
  ylabel('Error');
  

  
  I = 40;
  eta = 0.03;
  lambda = 0.0;
  E_tr = [];
  E_te = [];
  for kk = 1:10
    kk
    [e1, e2] = train_and_eval2(Rtrain, Rtest, max_m, max_n, kk, I, lambda, eta);
    e1
    e2
    E_tr = [E_tr; e1];
    E_te = [E_te; e2];
  end
  figure;
  plot(E_te)
  title(sprintf('V2 Test error with lambda = %f', lambda));
  xlabel('K');
  ylabel('Error');
  
  figure;
  plot(E_tr)
  title(sprintf('V2 Train error with lambda = %f', lambda));
  xlabel('K');
  ylabel('Error');

  
  I = 40;
  eta = 0.03;
  lambda = 0.2;
  E_tr = [];
  E_te = [];
  for kk = 1:10
    kk
    [e1, e2] = train_and_eval2(Rtrain, Rtest, max_m, max_n, kk, I, lambda, eta);
    E_tr = [E_tr; e1];
    E_te = [E_te; e2];
    e1
    e2
  end
  figure;
  plot(E_te)
  title(sprintf('V2 Test error with lambda = %f', lambda));
  xlabel('K');
  ylabel('Error');
  
  figure;
  plot(E_tr)
  title(sprintf('V2 Train error with lambda = %f', lambda));
  xlabel('K');
  ylabel('Error');
  
end

function [E_tr, E_te] = train_and_eval(Rtrain, Rtest, max_m, max_n, k, I, lambda, eta)
  scalar = sqrt(5 / k);
  Q = rand(max_m, k, 'double') * scalar;
  P = rand(max_n, k, 'double') * scalar;
  E = [];
  for i=1:I
    [Q, P] = SGD(Rtrain, Q, P, k, lambda, eta);
    e = error(Rtrain, Q, P, lambda);
    E = [E; e];
  end
  E_tr = error(Rtrain, Q, P, 0);
  E_te = error(Rtest, Q, P, 0);
end

function [Q, P] = SGD(R, Q, P, k, lambda, eta)
  [v_i, v_u, v_r] = find(R);
  for j = 1:size(v_u)
    u = v_u(j);
    i = v_i(j);
    R_iu = v_r(j);
    if R_iu == 0
      continue
    end
    epsilon_iu = R_iu - Q(i,:) * P(u,:)';
    new_qi = Q(i,:) + eta * (epsilon_iu * P(u,:));
    new_pu = P(u,:) + eta * (epsilon_iu * Q(i,:));
    new_qi = Q(i,:) + eta * (epsilon_iu * P(u,:) - lambda * Q(i,:));
    new_pu = P(u,:) + eta * (epsilon_iu * Q(i,:) - lambda * P(u,:));
    Q(i,:) = new_qi;
    P(u,:) = new_pu;
  end
end

function E = error(R, Q, P, lambda)
  E = 0;
  [v_i, v_u, v_r] = find(R);
  for j = 1:size(v_u)
    u = v_u(j);
    i = v_i(j);
    R_iu = v_r(j);
    E = E + (R_iu - Q(i,:) * P(u,:)')^2;
  end
  E = E + (sum(sum(P.^2)) + sum(sum(Q.^2))) * lambda;
end

function [E_tr, E_te] = train_and_eval2(Rtrain, Rtest, max_m, max_n, k, I, lambda, eta)
  scalar = sqrt(5 / k);
  Q = rand(max_m, k, 'double') * scalar;
  P = rand(max_n, k, 'double') * scalar;
  b_i = zeros(max_m, 1);
  sum_i = zeros(max_m, 1);
  b_u = zeros(max_n, 1);
  sum_u = zeros(max_n, 1);
  cnt = 0;
  sum = 0;
  [v_i, v_u, v_r] = find(Rtest);
  for j = 1:size(v_u)
    u = v_u(j);
    i = v_i(j);
    R_iu = v_r(j);
    b_i(i) = b_i(i) + R_iu;
    sum_i(i) = sum_i(i) + 1;
    b_u(u) = b_u(u) + R_iu;
    sum_u(u) = sum_u(u) + 1;
    cnt = cnt + 1;
    sum = sum + R_iu;
  end
  mu = sum / cnt;
  for i=1:max_m
    if sum_i(i) > 0
      b_i(i) = b_i(i) ./ sum_i(i) - mu;
    else
      b_i(i) = 0;
    end
  end
  for i=1:max_n
    if sum_u(i) > 0
      b_u(i) = b_u(i) ./ sum_u(i) - mu;
    else
      b_u(i) = 0;
    end
  end
  E = [];
  for i=1:I
    [Q, P, b_u, b_i] = SGD2(Rtrain, Q, P, mu, b_u, b_i, k, lambda, eta);
    e = error2(Rtrain, Q, P, mu, b_u, b_i, lambda);
    E = [E; e];
  end
  E_tr = error2(Rtrain, Q, P, mu, b_u, b_i, 0);
  E_te = error2(Rtest, Q, P, mu, b_u, b_i, 0);
end

%mu: universal bias. b_u: User bias. b_i: Item bias.
function [Q, P, b_u, b_i] = SGD2(R, Q, P, mu, b_u, b_i, k, lambda, eta)
  [v_i, v_u, v_r] = find(R);
  for j = 1:size(v_u)
    u = v_u(j);
    i = v_i(j);
    R_iu = v_r(j);
    if R_iu == 0
      continue
    end
    epsilon_iu = R_iu - (mu + b_u(u) + b_i(i) + Q(i,:) * P(u,:)');
    new_qi = Q(i,:) + eta * (epsilon_iu * P(u,:) - lambda * Q(i,:));
    new_pu = P(u,:) + eta * (epsilon_iu * Q(i,:) - lambda * P(u,:));
    Q(i,:) = new_qi;
    P(u,:) = new_pu;
    b_i(i) = b_i(i) + eta * (epsilon_iu - lambda * b_i(i));
    b_u(u) = b_u(u) + eta * (epsilon_iu - lambda * b_u(u));
  end
end

function E = error2(R, Q, P, mu, b_u, b_i, lambda)
  E = 0;
  [v_i, v_u, v_r] = find(R);
  for j = 1:size(v_u)
    u = v_u(j);
    i = v_i(j);
    R_iu = v_r(j);
    E = E + (R_iu - (mu + b_u(u) + b_i(i) + Q(i,:) * P(u,:)'))^2;
  end
  E = E + (sum(sum(P.^2)) + sum(sum(Q.^2)) + sum(b_i.^2) + sum(b_u.^2)) * lambda;
end



function [R, max_m, max_n, all_i, all_u] = init(file)
  max_m = 0;
  max_n = 0;
  MAX = 100000;
  R = sparse(MAX, MAX);
  all_i = sparse(MAX, 1);
  all_u = sparse(MAX, 1);
  fid = fopen(file);
  
  tline = fgets(fid);
  while ischar(tline)
    Rentry = sscanf(tline, '%d %d %d');
    u = Rentry(1);
    i = Rentry(2);
    if i > max_m
      max_m = i;
    end
    if u > max_n
      max_n = u;
    end
    R(i,u) = Rentry(3);
    all_i(i) = 1;
    all_u(u) = 1;
    tline = fgets(fid);
  end

  fclose(fid);           
end
