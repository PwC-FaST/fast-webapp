import { ApolloLink } from "apollo-link";
import { HttpLink } from "apollo-link-http";

const injectAuthorizationHeaderLink = new ApolloLink((operation, forward) => {
  let token = window.localStorage.getItem("fast_token");
  if (token === "null") {
    window.localStorage.removeItem("fast_token");
    token = null;
  }
  if (token) {
    operation.setContext({
      headers: {
        authorization: "JWT " + localStorage.getItem("fast_token")
      }
    });
  }
  return forward(operation);
});

const httpLink = new HttpLink({
  uri: "/graphql",
  headers: {}
});

const link = ApolloLink.from([injectAuthorizationHeaderLink, httpLink]);

export { link };
