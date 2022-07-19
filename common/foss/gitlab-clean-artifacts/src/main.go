package main

import (
	"fmt"
	"github.com/xanzy/go-gitlab"
	"io"
	"log"
	"os"
)

const UNIVERSE_PROJECT_ID = 20741933

// Remove artifacts for a job
func RemoveJobArtifacts(session *gitlab.Client, job_id int) {
	_, _, err := session.Jobs.DeleteArtifacts(
		UNIVERSE_PROJECT_ID,
		job_id,
	)
	if err != nil && err != io.EOF {
		log.Fatal(err)
	}
	fmt.Printf(
		"Artifacts for job %d removed.\n",
		job_id,
	)
}

func main() {

	// Login
	session, err := gitlab.NewClient(
		os.Getenv("UNIVERSE_API_TOKEN"),
	)
	if err != nil {
		log.Fatalf("Failed to create client: %v", err)
	}

	// Set basic options
	options := &gitlab.ListJobsOptions{
		ListOptions: gitlab.ListOptions{
			PerPage: 100,
			Page:    1,
		},
	}

	for {

		// Get page with jobs.
		jobs, resp, err := session.Jobs.ListProjectJobs(
			UNIVERSE_PROJECT_ID,
			options,
		)
		if err != nil {
			log.Fatal(err)
		}

		// Iterate over jobs
		for _, job := range jobs {
			if len(job.Artifacts) > 0 {

				// Concurrently remove artifacts
				go RemoveJobArtifacts(session, job.ID)
			}
		}

		// Iterate over pages
		if resp.NextPage > 0 {
			options.Page = resp.NextPage
		} else {
			break
		}
	}
}
