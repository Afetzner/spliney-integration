function vol = riemanns(data, distance)
    for i = 1: (size(data,1) - 1)
        for j = 1:(size(data,2) - 1)
            q(1, 1) = data(i, j);
            q(1, 2) = data(i+1, j);
            q(1, 3) = data(i, j+1);
            q(1, 4) = data(i+1, j+1);
            rMatSums(i, j) = mean(q);
        end
    end

    areaPerSquare = distance^2;
    rMatSumsArea = rMatSums * areaPerSquare;
    vol = sum(rMatSumsArea, 'all');
end