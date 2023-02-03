import http from "k6/http";
import { check, sleep } from "k6";

const API_TOKEN = __ENV["TEST_FORCES_TOKEN"];
const CI_COMMIT_REF_NAME = __ENV["CI_COMMIT_REF_NAME"];

const options = {
  stages: [
    { duration: "2m", target: 20 },
    { duration: "1m", target: 20 },
    { duration: "2m", target: 0 },
  ],
  thresholds: {
    http_req_duration: ["p(95)<5000"],
  },
};

const runTest = (): void => {
  const url = `https://${CI_COMMIT_REF_NAME}.app.fluidattacks.com/api`;
  const body = JSON.stringify({
    query: `
      query LoadTest {
        me {
          userName
          organizations {
            name
            groups {
              name
              findings {
                title
                vulnerabilitiesConnection {
                  edges {
                    node {
                      where
                      specific
                    }
                  }
                }
              }
            }
          }
        }
      }
    `,
  });
  const params = {
    headers: {
      authorization: `Bearer ${API_TOKEN}`,
      "content-type": "application/json",
    },
  };
  const response = http.post(url, body, params);

  check(response, {
    "status was 200": (resp) => resp.status == 200,
  });
  check(response, {
    "no errors": (resp) => {
      try {
        return JSON.parse(resp.body as string).errors === undefined;
      } catch {
        return false;
      }
    },
  });

  sleep(1);
};

export { options };
export default runTest;
