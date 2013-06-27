function r = main()
  % Single run. 
  find_nn_and_get_error(10, 24)
 
  % Plot error as a function of l.
  arr_l = 10:2:20;
  errs = [];
  for l = arr_l
    e = find_nn_and_get_error(l, 24);
    errs = [errs; e];
    l, e
  end
  plot(arr_l, errs)
  
  % Plot error as a function of k.
  arr_k = 16:2:24;
  errs = [];
  for k = arr_k
    e = find_nn_and_get_error(10, k);
    errs = [errs; e];
    k, e
  end
  plot(arr_k, errs)
  
  % Plot top 10 neighbours of patch 100 found by both methods.
  load patches
  T1=lsh('lsh',10,24,size(patches,1),patches,'range',255);
  [nnlsh,numcand] = lshlookup(patches(:,100),patches,T1,'k',11,'distfun','lpnorm','distargs',{1});
  figure(4);clf;
  for k=1:11, subplot(2,6,k);imagesc(reshape(patches(:,nnlsh(k)),20,20));colormap gray;axis image; end
  
  d = sum(abs(bsxfun(@minus,patches(:,100),patches))); [ignore,ind] = sort(d);
  figure(5);clf;
  for k=1:11, subplot(2,6,k);imagesc(reshape(patches(:,ind(k)),20,20));colormap gray;axis image; end
  
end

function e = find_nn_and_get_error(l, k)
  load patches
  T1=lsh('lsh',l,k,size(patches,1),patches,'range',255);

  % Compare run time of lsh and linear search.
  lsh_nn = [];
  tic;
  for i = 100:100:1000
    while true
      [nnlsh,numcand] = lshlookup(patches(:,i),patches,T1,'k',4,'distfun','lpnorm','distargs',{1});
      if size(nnlsh, 2) == 4
        break
      end
      size(nnlsh, 2)
    end
    lsh_nn = [lsh_nn; nnlsh];
  end
  toc
  linear_nn = [];
  tic;
  for i = 100:100:1000
    d = sum(abs(bsxfun(@minus,patches(:,i),patches)));
    [ignore,ind] = sort(d);
    linear_nn = [linear_nn; ind(1:4)];
  end
  toc

  % Measuring the error.
  e = error(lsh_nn, linear_nn, patches);
end


function e = error(lsh_nn, linear_nn, patches)
  a = 0;
  b = 0;
  e = 0;
  for j = 1:10
    for i = 2:4 
      a = a + dist(lsh_nn(j, i), lsh_nn(j, 1), patches);
      b = b + dist(linear_nn(j, i), linear_nn(j, 1), patches);
    end
    e = e + a / b;
  end
  e = e / 10;
end

function d = dist(a, b, patches)
 d = sum(abs(bsxfun(@minus,patches(:,a),patches(:,b))));
end

