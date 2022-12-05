samples = 61
flatMat = ones(samples, samples);
[X,Y] = meshgrid(0:1/(samples-1):1);


halfSlope = 1 - X + Y.*0;

bowlShape = X.^2 + Y.^2;

[X,Y] = meshgrid(-1:2/(samples-1):1);
bowlShape2 = X.^2 + Y.^2;

[X,Y] = meshgrid(0:1/(samples-1):1);
cubicShape = X.^3 + Y.^3;
surf(X,Y,cubicShape);