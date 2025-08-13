<script setup lang="ts">
import Navbar from "~/components/Navbar.vue";

</script>

<template>
  <UContainer>
    <Navbar />
    <main class="py-6">
      <slot />
    </main>
  </UContainer>
</template>


<style scoped>

</style>