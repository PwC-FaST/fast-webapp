import LoginPage from "@/components/login/LoginPage.vue";

function redirectIfNotLoggedIn({ component, options }) {
  return function(routeTo, routeFrom, resolve, reject) {
    let token = window.localStorage.getItem("fast_token");
    if (token && token !== "undefined") {
      console.log(
        "token ok, proceeding to",
        routeTo.path,
        "with component",
        component
      );
      resolve({ component, path: routeTo.path, options });
    } else {
      console.log("redirect to login");
      resolve({ component: LoginPage, path: "/login/" });
    }
  };
}

export { redirectIfNotLoggedIn };
