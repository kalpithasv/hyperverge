'use client';

import { GenerateAssessment } from '@/components/generate-assessment';
import { useParams } from 'next/navigation';

// Your GenerateAssessment component code here
export function GenerateAssessment(props: { adminId: string; courseId: string }) {
    return <GenerateAssessment adminId={props.adminId} courseId={props.courseId} />;

}