#ifndef MG_SRC_ECS_ARCHETYPE_H
#define MG_SRC_ECS_ARCHETYPE_H

#include "components.h"

namespace mg {
    typedef re::u32 EntityID;

    class Archetype {
    public:
        Archetype(
            const re::u32 component_count,
            const ComponentData* components,
            const re::u32 capacity
        );

        ~Archetype();

        Archetype(const Archetype&) = delete;
        Archetype(Archetype&&) = delete;

        Archetype& operator=(const Archetype&) = delete;
        Archetype& operator=(Archetype&&) = delete;

        EntityID createEntity();
        void destroyEntity(const EntityID entity_id);

        // TODO: Add iterator

    private:
        struct ArchetypeChunk {
            void* data = nullptr;
            ArchetypeChunk* next = nullptr;
        };

        re::u32 m_tail_size = 0;
        ArchetypeChunk* m_tail = nullptr;
        ArchetypeChunk* m_head = nullptr;

        re::u32 m_entity_size = 0;
        re::u32 m_chunk_data_size = 0;
        const re::u32 k_chunk_capacity;

        EntityID m_next_entity_id = 0;
    };
}

#endif