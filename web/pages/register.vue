<template>
  <div class="w-screen h-screen flex items-center justify-center">
    <AuthForm
        title="Register"
        buttonText="Sign Up"
        linkLabel="Already have an account? Login!"
        linkTarget="/login"
        @submit="handleRegister"
        class="max-w-[600px] w-full"
    />
  </div>
</template>

<script setup>
import { AuthServices } from "~/services/auth.js";
import { useRouter } from "vue-router";

definePageMeta({
  layout: 'auth'
})

const router = useRouter();

async function handleRegister(data) {
  const { res } = await AuthServices.register(data);
  if (res.status === 200) {
    alert("Register successfully.");
    router.push('/login')
    return
  }
  alert(`Register failed: ${data.detail}`)
}
</script>


<style scoped>

</style>