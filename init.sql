DROP table t315;
CREATE TABLE t315 as SELECT * from read_csv('data/results.csv', header=True);

select count(*) as "Leading In", "Leading Party" from t315 where Status = 'Result in Progress' group by "Leading Party" order by "Leading In";
select count(*) as "Trailing In", "Trailing Party" from t315 where Status = 'Result in Progress' group by "Trailing Party" order by "Trailing In";

select Constituency, "Leading Party", Margin, "Trailing Party", Round from t315 where Margin < 1000 order by Margin;

select count(*) as "Constituencies won", "Leading Party" from t315 where Status != 'Result in Progress' group by "Leading Party" order by "Constituencies won" desc;
