import { useState } from 'react';

interface GenerateAssessmentProps {
  adminId: string;
  courseId: string;
}

export default function GenerateAssessment({ adminId, courseId }: GenerateAssessmentProps) {
  const [form, setForm] = useState({
    role: '',
    skills: '',
    difficulty: 'Medium',
    include_minicase: true,
    include_aptitude: true,
  });
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    if (!form.role.trim() || !form.skills.trim()) {
      setError('Please fill in role and skills');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);
    
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/assessment/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...form,
          skills: form.skills.split(',').map(s => s.trim()).filter(s => s.length > 0),
        }),
      });
      
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || 'Failed to generate assessment');
      }
      
      const data = await res.json();
      if (!data.assessment || !data.coverage_report) {
        throw new Error('Invalid response format from server');
      }
      
      setResult(data);
    } catch (err: any) {
      setError(err.message || 'Unknown error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = (filename: string, content: any) => {
    const blob = new Blob([JSON.stringify(content, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-2xl font-light mb-8">Generate Assessment</h1>
      
      <div className="space-y-6 mb-8">
        <div>
          <input
            className="w-full px-4 py-3 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-black"
            placeholder="Role (e.g., Product Analyst)"
            value={form.role}
            onChange={e => setForm(f => ({ ...f, role: e.target.value }))}
          />
        </div>
        
        <div>
          <input
            className="w-full px-4 py-3 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-black"
            placeholder="Skills (comma separated, e.g., SQL, Product-Metrics)"
            value={form.skills}
            onChange={e => setForm(f => ({ ...f, skills: e.target.value }))}
          />
        </div>
        
        <div>
          <select
            className="w-full px-4 py-3 bg-white border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-black"
            value={form.difficulty}
            onChange={e => setForm(f => ({ ...f, difficulty: e.target.value }))}
          >
            <option value="Easy">Easy</option>
            <option value="Medium">Medium</option>
            <option value="Hard">Hard</option>
          </select>
        </div>
        
        <div className="flex gap-6">
          <label className="flex items-center cursor-pointer">
            <input
              type="checkbox"
              checked={form.include_minicase}
              onChange={e => setForm(f => ({ ...f, include_minicase: e.target.checked }))}
              className="mr-2"
            />
            Include Mini-Case
          </label>
          <label className="flex items-center cursor-pointer">
            <input
              type="checkbox"
              checked={form.include_aptitude}
              onChange={e => setForm(f => ({ ...f, include_aptitude: e.target.checked }))}
              className="mr-2"
            />
            Include Aptitude
          </label>
        </div>
        
        <button
          className="w-full px-6 py-3 bg-black text-white rounded-full font-light hover:opacity-90 transition-opacity cursor-pointer"
          onClick={handleGenerate}
          disabled={loading}
        >
          {loading ? 'Generating...' : 'Generate Assessment'}
        </button>
      </div>

      {error && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
          {error}
        </div>
      )}

      {result && (
        <div className="space-y-6">
          <div className="flex gap-3">
            <button
              className="px-4 py-2 bg-black text-white rounded-full font-light hover:opacity-90 transition-opacity cursor-pointer"
              onClick={() => handleDownload('assessment.json', result.assessment)}
            >
              Download Assessment
            </button>
            <button
              className="px-4 py-2 bg-black text-white rounded-full font-light hover:opacity-90 transition-opacity cursor-pointer"
              onClick={() => handleDownload('coverage_report.json', result.coverage_report)}
            >
              Download Coverage Report
            </button>
          </div>

          <div>
            <h2 className="text-xl font-light mb-4">Assessment Items</h2>
            <div className="space-y-4">
              {result.assessment.slice(0, 5).map((item: any, idx: number) => (
                <div key={idx} className="p-4 bg-gray-50 rounded-lg">
                  <div className="flex items-center gap-2 mb-2">
                    <span className="px-2 py-1 bg-black text-white text-xs rounded-full">
                      {item.type || 'Question'}
                    </span>
                    {item.difficulty && (
                      <span className="px-2 py-1 bg-gray-200 text-xs rounded-full">
                        {item.difficulty}
                      </span>
                    )}
                  </div>
                  <p className="text-sm mb-2">
                    {item.question || item.scenario || 'No question text'}
                  </p>
                  {item.choices && (
                    <div className="text-xs text-gray-600 mb-2">
                      <strong>Choices:</strong> {item.choices.join(', ')}
                    </div>
                  )}
                  {item.answer && (
                    <div className="text-xs text-gray-600">
                      <strong>Answer:</strong> {item.answer}
                    </div>
                  )}
                </div>
              ))}
              {result.assessment.length > 5 && (
                <p className="text-sm text-gray-500 text-center">
                  Showing first 5 of {result.assessment.length} items. Download for complete list.
                </p>
              )}
            </div>
          </div>

          <div>
            <h2 className="text-xl font-light mb-4">Coverage Report</h2>
            <pre className="p-4 bg-gray-50 rounded-lg text-sm overflow-x-auto">
              {JSON.stringify(result.coverage_report, null, 2)}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
}
