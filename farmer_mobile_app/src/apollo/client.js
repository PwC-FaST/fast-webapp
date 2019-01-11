import ApolloClient from "apollo-client/ApolloClient";
import { cache } from "./cache";
import { link } from "./link";

const client = new ApolloClient({
  link,
  cache,
  connectToDevTools: true
});

export { client };
