DROP table results;
CREATE TABLE results as SELECT * from read_csv('data/results.csv', header=True);

-- Predict who is leading
select count(*) as "Leading In", "Leading Party" from results where Status = 'Result in Progress' group by "Leading Party" order by "Leading In";

-- Predict what can change
select count(*) as "Trailing In", "Trailing Party" from results where Status = 'Result in Progress' group by "Trailing Party" order by "Trailing In";

-- Which Constituencies has very less margin -- Highly likely to change
select Constituency, "Leading Party", Margin, "Trailing Party", Round from results where Margin < 1000 order by Margin;

-- Declared results
select count(*) as "Constituencies won", "Leading Party" from results where Status != 'Result in Progress' group by "Leading Party" order by "Constituencies won" desc;
