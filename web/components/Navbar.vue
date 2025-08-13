<script setup lang="ts">

import { ref } from 'vue'
import type {NavigationMenuItem} from '@nuxt/ui'

const items = ref<NavigationMenuItem[]>([
  {
    label: 'Home',
    to: '/'
  }
])

</script>

<template>
  <UNavigationMenu :items="items" class="w-full justify-center"/>
</template>


<style scoped>

</style>