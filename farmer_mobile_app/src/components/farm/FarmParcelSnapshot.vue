<template>
  <div
    class="farm-snapshot-background"
    :style="{width: Math.round(this.width) + 'px', height: Math.round(this.height) + 'px'}"
  ></div>
</template>

<script>
export default {
  name: "farm-parcel-snapshot",
  props: {
    svg: { type: String, required: true },
    width: { type: Number, required: false, default: 100 },
    height: { type: Number, required: false, default: 100 }
  },
  mounted() {
    this.$el.innerHTML = this.svg;
    let svg = this.$el.getElementsByTagName("svg")[0];
    if (this.width) {
      svg.setAttribute("width", Math.round(this.width));
    }
    if (this.height) {
      svg.setAttribute("height", Math.round(this.height));
    }

    // Remove the inline attributes in the SVG so the formatting can be set by the .primary-parcel and
    // .secondary-parcel CSS classes
    function removeFormattingAttributes(x) {
      x.removeAttribute("stroke");
      x.removeAttribute("stroke-width");
      x.removeAttribute("stroke-opacity");
      x.removeAttribute("fill");
      x.removeAttribute("fill-opacity");
      x.removeAttribute("opacity");
    }

    new Array(...svg.getElementsByClassName("primary-parcel")).forEach(
      removeFormattingAttributes
    );
    new Array(...svg.getElementsByClassName("secondary-parcel")).forEach(
      removeFormattingAttributes
    );
  }
};
</script>

<style>
.farm-snapshot-background path.primary-parcel {
  stroke-width: 4px;
  stroke: #ffffff;
  stroke-opacity: 0;
  fill: #ffffff;
  fill-opacity: 1;
}

.farm-snapshot-background path.secondary-parcel {
  stroke-width: 8px;
  stroke: #ffffff;
  stroke-opacity: 0.8;
  fill: #ffffff;
  fill-opacity: 0.2;
}

.farm-snapshot-background {
  background: lightgrey;
  border: 1px solid silver;
}
</style>
