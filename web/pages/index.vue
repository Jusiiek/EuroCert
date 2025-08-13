<script setup lang="ts">
definePageMeta({
  layout: 'default'
})

</script>

<template>
  <div class="grid gap-4 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 p-4">
    <TaskCard title="Test title" description="Test description" />
    <TaskCard
        title="Test title very loing title omg Test title very loing title omg  Test title very loing title omg  "
        description="Test description Test description Test description Test description Test description Test description"
    />
  </div>
</template>


<style scoped>

</style>