def run_deep_dream_octaves(image2, network, steps_per_octave=100, step_size=0.02, octaves=4, octave_scale=1.5):
    img = tf.identity(image2)
    initial_shape = img.shape[:2]
    img = tf.convert_to_tensor(img)
    img = tf.image.resize(img, initial_shape)
    img = tf.cast(img, tf.float32)
    
    for octave in range(octaves):
        new_size = tuple([int(dim * (octave_scale ** octave)) for dim in initial_shape])
        img = tf.image.resize(img, new_size)
        print(f"Octave {octave+1}/{octaves}, image size: {img.shape}")
        for step in range(steps_per_octave):
            loss, img = deep_dream(network, img, step_size)
            if step % 50 == 0:
                print(f"  Step {step}/{steps_per_octave}, loss: {loss.numpy():.4f}")
        plt.figure(figsize=(8, 8))
        plt.imshow(inverse_transform(img))
        plt.axis('off')
        plt.title(f'Octave {octave+1}')
        plt.show()
    return img

# Executing DeepDream with octaves for more swirly, multi-scale effects
try:
    final_img = run_deep_dream_octaves(
        image2, 
        deep_dream_model, 
        steps_per_octave=100,   # More steps per octave = more detail
        step_size=0.01,         # Higher = more intense
        octaves=4,              # More octaves = more scales
        octave_scale=1.5        # How much to scale up each octave
    )
except Exception as e:
    print("Error during deep dream execution:", e)
