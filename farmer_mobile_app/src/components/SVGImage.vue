<template>
  <div class="svg-image" :style="style"></div>
</template>

<script>
let cache = new Map();

export default {
  name: "svg-image",
  props: {
    src: { type: String, required: true },
    width: { type: Number, required: false },
    height: { type: Number, required: false }
  },
  async mounted() {
    if (!cache.has(this.src)) {
      try {
        cache.set(this.src, fetch(this.src).then(r => r.text()));
      } catch (e) {
        cache.delete(this.src);
      }
    }
    if (cache.has(this.src)) {
      this.$el.innerHTML = await cache.get(this.src);
    }
  },
  computed: {
    style() {
      let s = {};
      if (this.width) {
        s.width = Math.round(this.width) + "px";
      }
      if (this.height) {
        s.height = Math.round(this.height) + "px";
      }
      return s;
    }
  }
};
</script>
