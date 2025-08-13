<script setup lang="ts">
import {ref} from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

interface NavItem {
  label: string
  to: string
}

const items = ref<NavItem[]>([
  {label: 'Home', to: '/'}
])
</script>


<template>
  <nav class="bg-[#018a52] h-[80px] px-4 py-2 rounded-b-lg shadow-md">
    <div class="container mx-auto flex justify-between items-center h-full">
      <div class="text-white font-bold text-xl hover:opacity-90 transition">
        EuroCert
      </div>

      <div class="flex items-center space-x-6">
        <NuxtLink
          v-for="link in items"
          :key="link.to"
          :to="link.to"
          :class="[
            'transition px-3 py-1 rounded hover:text-green-800 text-md font-bold',
            route.path === link.to
              ? 'underline underline-offset-4'
              : ''
          ]"
        >
          {{ link.label }}
        </NuxtLink>
      </div>
    </div>
  </nav>
</template>

<style scoped>

</style>