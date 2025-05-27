# User Data Sync - README

This document describes the workflow for synchronizing user files using the `d4wsync` client and a backend server.

## 1. Install the Sync App (Client Side)
Install the Sync application on the client's local machine.

## 2. Configure a Directory to Sync
Use the CLI to specify the local directory (D4W) to be synchronized.

## 3. Authenticate and Obtain JWT Token
Authenticate with the server to obtain a JWT token:

```bash
$ d4wsync auth -u client_id -p password
```

The server responds with a JWT token signed using its private key.

## 4. Update Server with Local File Metadata
Send information about local files (path, last modified datetime, and hash) to the server:

```bash
$ d4wsync update -all
```

The server saves this metadata to a Postgre database.

## 5. Get a List of Files to Sync
Request a list of files that need to be uploaded:

```bash
$ d4wsync get-sync-file
```

The server:
- Compares provided local metadata against the database
- Identifies files that have been modified or never uploaded
- Generates pre-signed AWS S3 URLs
- Sends the URLs back to the client

##  Upload Files to Temporary S3 Bucket
Upload all required files using the pre-signed URLs:

```bash
$ d4wsync upload -all
```

After each upload:
- The client sends a POST request to the server to confirm the upload
- The server updates the file's status in the database
- The pre-signed URL is invalidated/deleted

## 7. Virus Scan and File Processing (Server Side)
Once all files are uploaded to the **temporary S3 bucket**:
- The server runs a virus scan
- Malware is removed and reported
- Image files are processed (format conversion) directly within the temporary bucket

## 8. Move Files to Production S3 Bucket
Once scanning and processing are complete:
- The server uses the AWS CLI to copy files to the **production S3 bucket**
Since both buckets are in the **same AWS region**, this operation is fast and cost-effective
