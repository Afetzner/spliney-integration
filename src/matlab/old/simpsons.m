function vol = simpsons(data, distance)
    entries = size(data,1);
    coeff13 = coefficients(entries);
    h = distance * distance * 1/3 * 1/3;
    vol = h * sum(data.*coeff13, 'all');
end