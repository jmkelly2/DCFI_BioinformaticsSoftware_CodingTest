Task 1
Recursively find all FASTQ files in a directory and report each file name and the percent of sequences in that file that are greater than 30 nucleotides long.
Usage: python task1_fastq.py [path/file.fastq]
I first used os.walk to recursively find files with the fastq extension. For each file, I parsed the second line and every fourth line, which represent the sequence, and counted how many were > 30 in length. I then reported % of total that were counted for the condition as a string added to a list. I printed all report strings in the result list.
Result of the example files:
Reporting % sequences with > 30 nt per fastq file found:
./sample_files/fastq/read2/Sample_R2.fastq: 83.601%
./sample_files/fastq/read1/Sample_R1.fastq: 80.642%

Given a FASTA file with DNA sequences, find 10 most frequent sequences and return the sequence and their counts in the file.

Usage: python task1_fasta.py [path/file.fasta]
In the spirit of demonstrating use of data structures, I built a dictionary with sequences as keys and counts as items. I then sorted the list by count and took the top10, reporting the count and sequence.  Alternatively, the Counter class from the built-in collections could be used to clean up the code, as it makes a similar data structure to what I’ve implemented with cleaner code - but wouldn’t show off as much of my coding.
Result of example file:


Given a chromosome and coordinates, write a program for looking up its annotation. Keep in mind you'll be doing this annotation millions of times. Output Annotated file of gene name that input position overlaps.
I parsed the gtf myself by creating a dictionary indexed by chromosome. Each entry started as a dictionary indexed by gene name, with entries of (start_coordinate, end_coordinate) - the start and end coordinates were the min and max coordinate found in an annotation for each gene and were updated as the file was parsed. After the full gtf was parsed, the structure was collapsed into a dictionary indexed by (start, end, gene_name) and each index was sorted by start position. I chose to just store the gene and its start and stop positions since we were just interested in annotating coordinates with their overlapping genes.

I then parsed the input coordinates by looking up the chromosome index in my gtf dictionary, and performing a binary search to efficiently find genes with which the variant overlaps. If the input chromosome is not in the annotation, a warning is printed. I added the list of overlapping genes identified in the search as a column to the input tsv - with the final output as ANNOTATED_[input_file].
Output from the sample file is at sample_files/annotate/ANNOTATED_coordinates_to_annotate.txt

Task 2
Usage: python task2_coverage.py (optional -i [interval_filepath])

My instinct was to use pandas to solve this problem efficiently, but my solution was only a few lines of code. I included the pandas code in a comment at the top of my solution for reference. To demonstrate my programming skills, I wrote a function to parse the file per line and sort each interval into the appropriate GC content bin. I stored 2 lists of size 10 - one list to sum the coverage for each bin, and one list to keep track of the number of intervals in each bin. Index 0 of the lists stored the information for the [0-10)%GC bin, index 1 stored [10-20)%GC bin, etc.

Once the file was parsed, I looped through my bin lists and reported the sum(coverage)/count(intervals) per GC content bin. Below is my output for the sample file.

Mean coverage per GC content bin:
[0-10)% GC: 0.0
[10-20)% GC: 69.291
[20-30)% GC: 77.934
[30-40)% GC: 99.006
[40-50)% GC: 101.283
[50-60)% GC: 92.124
[60-70)% GC: 78.925
[70-80)% GC: 37.833
[80-90)% GC: 10.283
Task 3
Usage: python task3_ensemble.py [rsID_1],[rsID_2] (optional -o [filepath to output excel])

I wrote a script in Python to use the Ensembl REST API to query a list of input variants. I utilized the endpoint “/vep/human/id/” with the “ids:” message to get human variant effect annotations from a list of ids. I print the output json to the terminal, which could be directed to an output file. I also implemented an optional input argument to allow the user to output the result to excel, which converts the json to a pandas dataframe and saves it to excel.
Cloud Computing
How would you architect a framework for sharing large files (10Gb-25Gb) on the cloud with access controls at the file level? We want to share the same file with multiple users without making a copy. The users should be able to have access to the data on any cloud platform to run bioinformatics analysis pipelines. The users can run any cloud service, there is no restriction. The framework’s responsibility is only to make data accessible with access controls.
The files would be stored in a private storage bucket, such as Google Cloud Storage. A FastAPI backend service could be implemented in Python to act as the access control gateway. It would authenticate users via an identity provider like Okta using OAuth 2.0 and check file-level permissions against a metadata database. If the user is authorized, the API would generate an HMAC-signed URL that grants time-limited, read-only access to the file.
Users can pass the signed URL directly to bioinformatics pipelines without needing to move or duplicate data. This setup supports reproducible, scalable workflows and meets security and compliance needs while remaining cloud-agnostic.

Evaluate the benefits and limitations of using containerization and container orchestration technologies, such as Docker and Kubernetes, for deploying and managing bioinformatics HPC workloads in the cloud.
Benefits:
- Docker: Encapsulates tools and dependencies, ensuring consistent execution and easy portability across environments.
- Kubernetes: Enables automated job scheduling and scaling, making it easy to parallelize workflows.
- Easily integrates with cloud platforms like Terra, DNAnexus, or custom pipelines on GCP, AWS, or Azure, facilitating scalable, reproducible analyses.

Limitations:
I/O-bound tasks - common in bioinformatics when working with very large files - are slowed down due to performance limitations of cloud storage.
High network latency and the lack of low-latency interconnects in cloud environments can hinder the performance of parallel computing tasks that require tight node coordination.
Overhead of setting up Docker and Kubernetes can be inefficient for small, quick jobs that don’t require containerization or orchestration benefits like scalability.

SQL
Incorrect:				
SELECT UserId, AVG(Total) AS AvgOrderTotal FROM Invoices
HAVING COUNT(OrderId) >= 1 
Problem: This statement is trying to select the user IDs and average totals of orders for users with more than one order. In order to count the orders per user and filter for >= 1, “HAVING” and “COUNT” need to be used with invoices (rows) that have first been grouped by user ID using “GROUP BY”. This also allows the average total to be calculated per user.

The correct statement should be:
SELECT UserId, AVG(Total) AS AvgOrderTotal FROM Invoices
GROUP BY UserId
HAVING COUNT(OrderId) >= 1 		
