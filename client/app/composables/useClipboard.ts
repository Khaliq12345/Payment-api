export const useClipboard = () => {
  const toast = useToast();

  const copyToClipboard = async (text: string) => {
    const successTitle = "Lien copié !";
    const successIcon = "i-lucide-check-circle";
    const errorTitle = "Échec de la copie";
    const errorDescription = "Veuillez copier manuellement";
    const errorIcon = "i-lucide-x-circle";
    const showToast = true;

    try {
      // Quick check for Clipboard API availability
      if (navigator.clipboard && navigator.clipboard.writeText) {
        await navigator.clipboard.writeText(text);
      } else {
        // Fallback for non-HTTPS environments
        const textArea = document.createElement("textarea");
        textArea.value = text;
        textArea.style.position = "fixed";
        textArea.style.left = "-999999px";
        textArea.style.top = "-999999px";
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();

        const successful = document.execCommand("copy");
        textArea.remove();

        if (!successful) {
          throw new Error("Fallback copy failed");
        }
      }

      // Show success notification
      if (showToast) {
        toast.add({
          title: successTitle,
          icon: successIcon,
          color: "primary",
        });
      }

      return true;
    } catch (err) {
      console.error("Échec de la copie : ", err);

      if (showToast) {
        toast.add({
          title: errorTitle,
          description: errorDescription,
          icon: errorIcon,
          color: "error",
        });
      }

      return false;
    }
  };

  return {
    copyToClipboard,
  };
};
