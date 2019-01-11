import {
  InMemoryCache,
  IntrospectionFragmentMatcher
} from "apollo-cache-inmemory";
import schema from "./schema";
import { CachePersistor } from "apollo-cache-persist";
import localforage from "localforage";

// Ids for data normalization
function dataIdFromObject(object) {
  // FarmType has a special treatment as we for the moment assume that each farmer has only a single farm
  // obviously this will break if there are multiple farms created in the admin interface for the same farmer.
  if (object.id && object.__typename !== "FarmType") {
    return object.__typename + "." + object.id;
  } else {
    return object.__typename;
  }
}

// This is necessary as we are using UNION types for the home feed
// see https://www.apollographql.com/docs/react/advanced/fragments.html#fragment-matcher
const fragmentMatcher = new IntrospectionFragmentMatcher({
  introspectionQueryResultData: {
    __schema: {
      types: schema.data.__schema.types.filter(x => x.possibleTypes)
    }
  }
});

// Instantiate the cache
const cache = new InMemoryCache({
  fragmentMatcher,
  addTypename: true,
  dataIdFromObject
});

// The in-cache persistence to local storage
const persistor = new CachePersistor({
  cache,
  storage: localforage
});

export { cache, persistor };
