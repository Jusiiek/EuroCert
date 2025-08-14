<template>
  <div class="w-screen h-screen flex items-center justify-center">
    <UCard class="w-full max-w-md p-6">
      <template #header>
        <h2 class="text-xl font-bold text-center">{{ title }}</h2>
      </template>

      <UForm @submit="submitForm" :state="form" class="flex flex-col items-center">
        <UFormGroup class="w-full mb-4">
          <label for="email" class="block text-md font-medium mb-1 text-gray-400">Email</label>
          <UInput
            id="email"
            v-model="form.email"
            type="email"
            placeholder="Enter your email"
            class="w-full"
          />
        </UFormGroup>

        <UFormGroup class="w-full mb-4">
          <label for="password" class="block text-md font-medium mb-1 text-gray-400">Password</label>
          <UInput
            id="password"
            v-model="form.password"
            type="password"
            placeholder="Enter your password"
            class="w-full"
          />
        </UFormGroup>

        <div class="w-full flex justify-center">
          <UButton type="submit" class="mt-4 w-auto px-6">{{ buttonText }}</UButton>
        </div>
        <div class="w-full flex justify-center mt-2">
          <NuxtLink :to="linkTarget" class="hover:text-[#05df72]">
            {{ linkLabel }}
          </NuxtLink>
        </div>
      </UForm>
    </UCard>
  </div>
</template>

<script setup>
const props = defineProps({
  title: String,
  buttonText: String,
  linkLabel: String,
  linkTarget: String,
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