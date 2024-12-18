<template>
    <header class="settings-header">
        <Logo title="USER MANAGEMENT" />

        <div class="settings-header-actions">
            <button @click="logout()" class="button button-primary">Logout</button>
        </div>
    </header>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import Logo from './Logo.vue'

const router = useRouter()

const logout = async () => {
    try {
        await axios.post('/api/logout')
        router.push('/login')
    } catch (error) {
        console.error("Error during logout:", error)
    }
}
</script>