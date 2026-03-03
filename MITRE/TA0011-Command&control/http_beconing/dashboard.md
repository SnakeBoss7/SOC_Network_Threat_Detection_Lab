## Panel 1
**beconing detection**
```
index="zeek" sourcetype="bro:http:json" latest=-1d
| sort 0 id.orig_h id.resp_h _time
| streamstats current=f last(_time) as prev_time by id.orig_h id.resp_h uri
| eval interval = _time - prev_time
| where interval > 0
| stats count avg(interval) as avg_interval stdev(interval) as stand_dev min(interval) as min_interval max(interval) as max_interval by id.orig_h id.resp_h 
| eval coff_variance = stand_dev/avg_interval
| where count > 20 AND coff_variance < 0.3
```

## Panel 2
**Beaconing Timeline**
```
index="zeek" sourcetype="bro:http:json" id.orig_h="10.10.10.5" id.resp_h="10.10.10.2"
| timechart span=1m count by uri

```
## Panel 3
**Top 5 Talkers**
```
index="zeek" sourcetype="bro:http:json"
| stats count by id.orig_h id.resp_h
| chart sum(count) over id.orig_h by id.resp_h
| head 5

```
## Panel 4
**Top 5 User-Agents**
```
index="zeek" sourcetype="bro:http:json"
| stats count by user_agent
| sort -count
| head 5
```