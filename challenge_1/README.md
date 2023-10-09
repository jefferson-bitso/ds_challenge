# DS Challenge 1

The partition key used for the data lake was the timestamp, which would distribute the data across the nodes based on the year/month/day.
That way, we would improve the performance of queries using a large range of time, since the load would be split across many worker nodes.

Some logic must be implement to evaluate the pre-existing data before running a new load (Unfortunatelly the time didn't allowed me to conclude this piece)
