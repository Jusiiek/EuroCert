<script setup lang="ts">
import Navbar from "~/components/Navbar.vue";
</script>


<template>
  <div>
    <Navbar/>
    <UContainer>
      <main class="py-6">
        <slot/>
      </main>
    </UContainer>
  </div>

</template>

<style scoped>

</style>