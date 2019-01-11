import VueApollo from "vue-apollo";
import { client } from "./client";

const provider = new VueApollo({
  defaultClient: client
});

export { provider };
