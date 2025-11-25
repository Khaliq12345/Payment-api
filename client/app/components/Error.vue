<template>
    <div
        class="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 px-4"
    >
        <div class="text-center">
            <!-- 404 Number -->
            <h1 class="text-9xl font-black text-gray-900 dark:text-white mb-4">
                404
            </h1>

            <!-- Main Message -->
            <h2
                class="text-3xl font-semibold text-gray-800 dark:text-gray-200 mb-3"
            >
                Oups, cette page est introuvable !
            </h2>

            <!-- Description -->
            <p class="text-gray-500 dark:text-gray-400 mb-2">
                Le lien est peut-être corrompu,
            </p>

            <p class="text-sm text-gray-600 dark:text-gray-500 mb-8">
                ou la page a peut-être été supprimée
            </p>

            <!-- Button -->
            <UButton
                label="RETOUR À L'ACCUEIL"
                color="neutral"
                variant="solid"
                size="lg"
                @click="navigateTo('/')"
            />
        </div>
    </div>
</template>

<script setup lang="ts"></script>
