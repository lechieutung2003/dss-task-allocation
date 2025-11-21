<template>
  <div class="p-6 rounded-lg shadow-lg flex-1 flex-col" :class="bgClass">
    <div class="justify-between items-center flex mb-3">
      <div
        class="inline-flex items-center capitalize leading-none text-xs border rounded-full py-1 px-3 bg-emerald-500 border-emerald-500 text-white mt-2"
        v-if="percentage !== undefined"
        :class="statusClass"
      >
        <span class="mr-1" :class="iconClass">
          <component
            :is="statusIcon"
            style="width: 1em; height: 1em; margin-right: 8px"
          />
        </span>
        <span>{{ percentage }}%</span>
      </div>
    </div>
    <div class="flex flex-row justify-between items-center">
      <div>
        <h3 class="text-lg font-semibold" :class="textClass">
          {{ title }}
        </h3>
        <p class="text-2xl font-bold mt-1" :class="textClass">
          {{ value }}
        </p>
        <p v-if="subtitle" class="text-sm mt-1 opacity-80" :class="textClass">
          {{ subtitle }}
        </p>
      </div>
      <component
        :is="iconComponent"
        class="text-2xl h-16"
        :class="iconClass"
        style="width: 2em; height: 2em"
      />
    </div>
  </div>
</template>
<script setup lang="ts">
import { CaretTop, CaretBottom, DCaret } from "@element-plus/icons-vue";
const props = defineProps({
  title: {
    type: String,
    required: true,
  },
  value: {
    type: [String, Number],
    required: true,
  },
  subtitle: {
    type: String,
    default: "",
  },
  percentage: {
    type: Number,
    default: undefined,
  },
  status: {
    type: String,
    default: "neutral", // "positive", "negative", "neutral"
  },
  bgClass: {
    type: String,
    default: "bg-white",
  },
  textClass: {
    type: String,
    default: "text-gray-800",
  },
  iconClass: {
    type: String,
    default: "text-gray-400",
  },
  iconComponent: {
    type: [Object, Function, String],
    required: true, // Pass the icon as a component
  },
  // statusIcon: {
  //   type: [Object, Function, String],
  //   default: null, // Optional icon for status
  // },
});

const statusClass = computed(() => {
  switch (props.status) {
    case 'positive':
      return 'bg-green-500 border-green-500 text-white';
    case 'negative':
      return 'bg-red-500 border-red-500 text-white';
    default:
      return 'bg-gray-500 border-gray-500 text-white';
  }
});

const statusIcon = computed(() => {
  switch (props.status) {
    case 'positive':
      return CaretTop;
    case 'negative':
      return CaretBottom;
    default:
      return DCaret;
  }
});
</script>
