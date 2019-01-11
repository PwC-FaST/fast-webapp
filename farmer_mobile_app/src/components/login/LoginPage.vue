<template>
  <f7-page no-toolbar no-navbar no-swipeback login-screen>
    <div class="text-align-center bg-color-gray6" style="padding: 40px 0">
      <img src="/static/farmer_mobile_app/img/logo.svg" width="80">
      <h2 class="no-margin-bottom">Farm Sustainability Tool</h2>
    </div>
    <f7-block></f7-block>
    <f7-list form>
      <f7-list-input
        label="Username"
        type="text"
        placeholder="Your username"
        :value="username"
        @input="username = $event.target.value"
      ></f7-list-input>
      <f7-list-input
        label="Password"
        type="password"
        placeholder="Your password"
        :value="password"
        @input="password = $event.target.value"
      ></f7-list-input>
    </f7-list>
    <p v-if="error" class="text-align-center text-color-red">{{ error }}</p>
    <f7-list>
      <f7-list-button big fill @click="signIn">Sign In</f7-list-button>
      <f7-block-footer>Please enter your FaST credentials</f7-block-footer>
    </f7-list>
  </f7-page>
</template>

<script>
import mutationTokenAuth from "./graphql/mutationTokenAuth.gql";
import { client } from "@/apollo/client";
import { persistor } from "@/apollo/cache";

export default {
  name: "login-page",
  data() {
    return {
      username: "",
      password: "",
      error: null
    };
  },
  methods: {
    signIn() {
      let preloader = this.$f7.dialog.preloader(
        "Signing in..."
      );
      this.$apollo
        .mutate({
          mutation: mutationTokenAuth,
          variables: {
            username: this.username.toLowerCase(),
            password: this.password
          }
        })
        .then(data => {
          this.error = null;
          const token = data.data.tokenAuth.token;
          window.localStorage.setItem("fast_token", token);

          if (token) {

            // Reset the cache
            client.cache.reset();

            // Resume the persistence
            persistor.resume();
            preloader.close();
            
            // Navigate to home page
            this.$f7router.navigate("/", { reloadAll: true, clearPreviousHistory: true, ignoreCache: true });

            // Resume all queries
            this.$apollo.skipAll = false
            
          } else {
            preloader.close();
            window.localStorage.setItem("fast_token", null);
            this.error = "Could not sign you in, please try again";
            }
        })
        .catch(error => {
          preloader.close();
          window.localStorage.setItem("fast_token", null);
          this.error = "Invalid credentials";
        });
    }
  }
};
</script>
