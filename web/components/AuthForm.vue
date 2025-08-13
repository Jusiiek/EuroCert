<template>
  <UCard>
    <template #header>
      <h2 class="text-xl font-bold">{{ title }}</h2>
    </template>

    <UForm @submit="submitForm" :state="form">
      <UFormGroup label="Email" name="email">
        <UInput v-model="form.email" type="email" placeholder="Enter your email" />
      </UFormGroup>

      <UFormGroup label="Password" name="password">
        <UInput v-model="form.password" type="password" placeholder="Enter your password" />
      </UFormGroup>

      <UButton type="submit" class="mt-4" block>{{ buttonText }}</UButton>
    </UForm>
  </UCard>
</template>

<script setup>
const props = defineProps({
  title: String,
  buttonText: String
})

const emit = defineEmits(["submit"])

const form = reactive({
  email: "",
  password: ""
})

function submitForm() {
  emit("submit", { ...form })
}
</script>

<style scoped>

</style>