<script setup lang="ts">
import Navbar from "~/components/Navbar.vue";
</script>


<template>
  <div>
    <Navbar/>
    <UContainer>
      <div class="py-6">
        <slot/>
      </div>
    </UContainer>
  </div>

</template>

<style scoped>

</style>