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
Gamma = Su * R;
[top5, top5_idx] = sort(Gamma(idx_alex, 1:100), 'descend');

Si = Q^(-1/2)*R'*R*Q^(-1/2);
Gamma = R * Si;
[top5, top5_idx] = sort(Gamma(idx_alex, 1:100), 'descend');
